import plotly.graph_objs as go

def create_axis_descriptor(axis, unit=None):
    return axis + (" [%s]" % (unit if unit else "-"))


def scatterplot_from_df(df, xCol, yCol, seriesCol="", includeSpecific=[], nameCols=[], xUnit="", yUnit="", connect=False):
    def create_plot_series(name=""):
        series = df.loc[df.loc[:,seriesCol] == name] if seriesCol and name else df
        
        return {
            'x': series.loc[:,xCol], 
            'y': series.loc[:,yCol], 
            'text': (
                series.loc[:,nameCols].apply(
                    lambda x: ", ".join(
                        ["%s: %s"%(name, x.loc[name]) for name in nameCols]
                        ),
                        axis="columns"
                    )
                if nameCols else None
                ),
            'name': name,
            'type': "scatter",
            'mode': ("lines+" if connect else "")+"markers"
        }
    
    return ({
        'data': (
            [
                create_plot_series(name=name) 
                for name in df.loc[:,seriesCol].unique()
                if not includeSpecific or name in includeSpecific
            ] 
            if seriesCol 
            else [create_plot_series()]
        ),
        'layout': {
            'xaxis': {'title': create_axis_descriptor(xCol, xUnit)},
            'yaxis': {'title': create_axis_descriptor(yCol, yUnit)}
        }
    })

def boxplot_from_df(df, valueCol, seriesCol="", includeSpecific=[], valueUnit=""):
    def create_plot_series(name=""):
        series = df.loc[df.loc[:,seriesCol] == name] if seriesCol and name else df
        
        return {
            'y': series.loc[:,valueCol], 
            'name': name, 
            'type': "box"
        }
    
    return ({
        'data': (
            [
                create_plot_series(name=name) 
                for name in df.loc[:,seriesCol].unique()
                if not includeSpecific or name in includeSpecific
            ] 
            if seriesCol 
            else [create_plot_series()]
        ),
        'layout': {
            'yaxis': {'title': create_axis_descriptor(valueCol, valueUnit)}
        }
    })