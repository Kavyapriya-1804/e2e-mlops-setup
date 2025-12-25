import os
import pandas as pd
from model_monitoring.evidently_monitoring import Monitoring, DataSummaryReport, RegressionReport, Regression
from evidently.sdk.panels import DashboardPanelPlot
from evidently.sdk.models import PanelMetric
from create_online_feature import CreateOnlineFeatures
from sklearn.model_selection import train_test_split
from model_serving.model_serving import BentoModel

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

def add_dashboards(project):
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="House price Monitoring dashboard",
            size="full", 
            values=[], #leave empty
            plot_params={"plot_type": "text"},
        ),
        tab="House price Monitoring", #will create a Tab if there is no Tab with this name
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Row count",
            subtitle="Total number of evaluations over time.",
            size="half",
            values=[PanelMetric(legend="Row count", metric="RowCount")],
            plot_params={"plot_type": "counter", "aggregation": "sum"},
        ),
        tab="Sum",
    )

    # Average
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Row count",
            subtitle="Average number of evaluations per Report.",
            size="half",
            values=[PanelMetric(legend="Row count", metric="RowCount")],
            plot_params={"plot_type": "counter", "aggregation": "avg"},
        ),
        tab="Average",
    )

    # Last
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Row count",
            subtitle="Latest number of evaluations.",
            size="half",
            values=[PanelMetric(legend="Row count", metric="RowCount")],
            plot_params={"plot_type": "counter", "aggregation": "last"},
        ),
        tab="Last",
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Row count",
            subtitle="Total number of evaluations over time.",
            size="half",
            values=[PanelMetric(legend="Row count", metric="RowCount")],
            plot_params={"plot_type": "pie", "aggregation": "sum"},
        ),
        tab="Pie Chart",
    )
    # line chart
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Row count",
            subtitle = "Number of evaluations over time.",
            size="half",
            values=[
                PanelMetric(
                    legend="Row count",
                    metric="RowCount",
                ),
            ],
            plot_params={"plot_type": "line"},
        ),
        tab="Line Chart",
    )
            
    # bar chart
    project.dashboard.add_panel(
            DashboardPanelPlot(
            title="Row count",
            subtitle = "Number of evaluations over time.",
            size="half",
            values=[
                PanelMetric(
                    legend="Row count",
                    metric="RowCount",
                ),
            ],
            plot_params={"plot_type": "bar", "is_stacked": False}, #default False, set as True to get stacked bars
        ),
        tab="Bar Chart",
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Text Length",
            subtitle="Text length stats (symbols).",
            size="full",
            values=[
                PanelMetric(legend="max", metric="MaxValue", metric_labels={"column": "length"}),
                PanelMetric(legend="mean", metric="MeanValue", metric_labels={"column": "length"}),
                PanelMetric(legend="min", metric="MinValue", metric_labels={"column": "length"}),
            ]
        )
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Row count",
            subtitle = "Number of evaluations over time.",
            size="half",
            values=[
                PanelMetric(
                    legend="Row count",
                    metric="RowCount", ## <- metric name
                ),
            ],
            plot_params={"plot_type": "line"},
        ),
        tab="My tab",
    )



if __name__ == "__main__":
    create_online_feature = CreateOnlineFeatures()

    feature_store_path = os.path.join(str(PROJECT_ROOT) + "/feature_store/feature_repo")
    print(create_online_feature.set_feature_store(feature_store_path))

    print("-----")

    online_datasource_path = os.path.join(str(PROJECT_ROOT) + "/data/house_target.parquet")
    print(create_online_feature.set_entity_df(online_datasource_path))

    print("-----")

    entity_df = create_online_feature.get_entity_df()
    target = entity_df["price"]
    print(target)

    print("-----")

    # online_df = create_online_feature.get_online_df()
    online_df = pd.read_csv("data/Housing_processed.csv")
    # online_features = online_df.drop(labels=["house_id"], axis=1)
    online_features = online_df[["bedrooms",  "mainroad", "area"]]
    # online_features.dropna()
    print(online_features)

    print("-----")

    X_train, X_test, y_train, y_test = train_test_split(online_features, target, test_size=0.2, random_state=42)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

    print("-----")

    monitoring = Monitoring()

    ws = monitoring.create_workspace("House Price Monitoring Workspace")
    project = monitoring.search_or_create_project("House Price Monitoring Project", ws)
    print(project)

    print("-----")

    reference = X_train.copy()
    reference['price'] = y_train.copy()

    current = X_test.copy()
    current['price'] = y_test.copy()

    monitoring.set_schema(numerical_columns=['area', 'bedrooms', 'price'], categorical_columns=['mainroad'], regression=None)
    print(monitoring.current_strategy)
    
    print("-----")

    drift_report = monitoring.execute_strategy(reference, current, ws)
    print(drift_report.dict())
    
    print("-----")

    monitoring.set_strategy = DataSummaryReport()
    print(monitoring.current_strategy)

    print("-----")

    data_summary_report = monitoring.execute_strategy(reference, current, ws)
    print(data_summary_report.dict())

    print("-----")

    bento_model = BentoModel()
    model = bento_model.load_model(model_name="house_price_model:latest")

    reference_with_pred = reference.copy()
    y_train_pred = model.predict(X_train)
    reference_with_pred['predicted_price'] = y_train_pred

    y_pred = model.predict(X_test)
    current_with_pred = current.copy()
    current_with_pred['predicted_price'] = y_pred

    monitoring.set_strategy = RegressionReport()
    print(monitoring.current_strategy)

    print("-----")

    regression=[
        Regression(target="price", prediction="predicted_price"),
    ]
    monitoring.set_schema(numerical_columns=['area', 'bedrooms', 'price'], categorical_columns=['mainroad'], regression=regression)

    reg_report = monitoring.execute_strategy(reference_with_pred, current_with_pred, ws)
    print(reg_report.dict())

    print("-----")

    add_dashboards(project)
    print("Dashboards added to report successfully")

    print("-----")
