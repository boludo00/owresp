import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools


class Grapher(object):

    def __init__(self):
        py.sign_in("boludo00", "caCJFQ3nYafwrCXikwVv")
        

    def horizontal_bar(self, x, y):
        """
        Given an x axis and categorical y axis, plot a horizontal bar graph
        and save it as a png in the local directory.
        :param x: array like, the x values to plot
        :param y: array like, the y labels 
        """
        data = [go.Bar(
            x=x,
            y=y,
            orientation = 'h'
        )]
        fig = go.Figure(data=data)
        return py.image.save_as(fig, filename='horizontal-bar.png')

    def multiple_tiles(self, herostats):
        """
        Generates a grid of an overview of horizontal barcharts. 

        :param herostats: The iterable of HerosStats to visualize.
        """
        assert len(herostats) == 6, "expected list of %d HerosStats instances, got %d" % (6, len(herostats))
        titles = map(lambda hs: hs.stat_name, herostats)
        fig = tools.make_subplots(rows=3, cols=2, subplot_titles=titles)

        j = 0
        k = 1
        for i, hs in enumerate(herostats):
            if i % 2 != 0:
                k = 2
            else:
                k = 1
                j += 1
            trace = go.Bar(x=zip(*hs)[1], y=zip(*hs)[0], orientation='h')
            fig.append_trace(trace, 1*j, k)

        fig['layout'].update(height=600, width=600, title='Hero Overview', showlegend=False)

        py.image.save_as(fig, filename='make-subplots-multiple-with-titles.png')

