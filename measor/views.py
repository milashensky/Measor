from measor.mixins import TemplateView


class IndexView(TemplateView):
    template_name = 'base.html'
    methods = ['GET']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
