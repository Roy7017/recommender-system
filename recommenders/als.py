import implicit
import surprise
import pandas as pd
import numpy as np
import scipy.sparse as sparse

class ImplicitAlternatingLeastSquares(implicit.als.AlternatingLeastSquares):
    def __init__(
        self,
        factors=100,
        regularization=0.01,
        dtype=np.float32,
        use_native=True,
        use_cg=True,
        use_gpu=implicit.cuda.HAS_CUDA,
        iterations=15,
        calculate_training_loss=False,
        num_threads=0,
        random_state=None,
        alpha=40, 
    ):
        super().__init__(
            factors=factors,
            regularization=regularization,
            dtype=dtype,
            use_native=use_native,
            use_cg=use_cg,
            use_gpu=use_gpu,
            iterations=iterations,
            calculate_training_loss=calculate_training_loss,
            num_threads=num_threads,
            random_state=random_state,
        )
        self.global_baseline_model = surprise.BaselineOnly()
        self.alpha = alpha

    def fit(self, train_data, show_progress=True):
        self.train_data = train_data.copy()
        self.reader = surprise.Reader(rating_scale=(0, self.train_data['size'].max()))
        self.train_dataset = surprise.Dataset.load_from_df(
            self.train_data[["user", "service", "size"]], self.reader
        )
        self.global_baseline_model.fit(self.train_dataset.build_full_trainset())

        self.users: list = train_data["user"].unique()
        self.services: list = train_data["service"].unique()

        self.uid_to_idx = {user: index for index, user in enumerate(self.users)}
        self.idx_to_uid = {index: user for index, user in enumerate(self.users)}

        self.iid_to_idx = {item: index for index, item in enumerate(self.services)}
        self.idx_to_iid = {index: item for index, item in enumerate(self.services)}

        self.train_data["baseline"] = self.train_data.apply(
            self.get_baseline, axis=1, bi=self.global_baseline_model.bi, bu=self.global_baseline_model.bu, mean=self.train_data['size'].mean()
        )

        self.train_data["confidence"] = self.train_data["baseline"].apply(
            lambda baseline: 1 + (baseline * self.alpha)
        )

        cat_type = pd.api.types.CategoricalDtype(categories=self.users)
        self.rows = self.train_data.user.astype(cat_type).cat.codes
        # Get the associated row indices

        cat_type = pd.api.types.CategoricalDtype(categories=self.services)
        self.cols = self.train_data.service.astype(cat_type).cat.codes
        # Get the associated column indices
        
        confidence = list(self.train_data.confidence)  # All of our confidence values

        self.confidence_sparse = sparse.csr_matrix(
            (confidence, (self.rows, self.cols)), shape=(len(self.users), len(self.services))
        )

        return super().fit(self.confidence_sparse.transpose().tocsr(), show_progress=show_progress)

    def rank_items(self, recalculate_user=False):
        implicit_als_rankings = {}
        for (user, user_index) in self.uid_to_idx.items():
            rankings = super().rank_items(
                userid=user_index,
                user_items=self.confidence_sparse,
                selected_items=list(self.idx_to_iid.keys()),
                recalculate_user=recalculate_user,
            )
            implicit_als_rankings[user] = [self.idx_to_iid[index] for (index, score) in rankings]
        return implicit_als_rankings

    def get_baseline(self, row, bi: np.ndarray, bu: np.ndarray, mean):
        size = row["size"]
        uid: str = row["user"]
        iid: str = row["service"]
        user_index = self.uid_to_idx[uid]
        item_index = self.iid_to_idx[iid]
        return size - mean - bi[item_index] - bu[user_index]
