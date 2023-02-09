import pandas as pd


class MetricBuilder:
    def __init__(self):
        self.name = None
        self.type = None
        self.feature = None
        self.action = None
        self.label = None
        self.description = None
        self.total = None

    def with_name(self, name):
        self.name = name
        return self

    def with_type(self, type):
        self.type = type
        return self

    def with_feature(self, feature):
        self.feature = feature
        return self

    def with_action(self, action):
        self.action = action
        return self

    def with_label(self, label):
        self.label = label
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_total(self, total):
        self.total = total
        return self

    def with_dataframe_a(self, dataframe, metric_pandas):
        metrics = []
        if isinstance(dataframe, pd.DataFrame):
            for index, row in dataframe.iterrows():
                try:
                    total = metric_pandas.extract_total(row["metric"])
                    if not total:
                        total = 0
                    metrics.append(
                        MetricBuilder()
                        .with_name(row["metric"])
                        .with_type(row["type"])
                        .with_feature(row["feature"])
                        .with_action(row["action"])
                        .with_label(row["label"])
                        .with_description(row["description"])
                        .with_total(total)
                        .build()
                    )
                except Exception as e:
                    pass
        return metrics

    def build(self):
        return Metric(self)


class Metric:
    def __init__(self, builder):
        self.name = builder.name
        self.type = builder.type
        self.feature = builder.feature
        self.action = builder.action
        self.label = builder.label
        self.description = builder.description
        self.total = builder.total

    def __str__(self):
        return f"{self.__dict__}"
