# -*- coding: utf-8 -*-

from hipflask import has_text, has_elements, HipflaskException


class CannotFindViewException(HipflaskException):
    """
    Thrown in response to failing to find a named view.
    """

    def __init__(self, message, cause=None):
        super(CannotFindViewException, self).__init__(message, cause)

    @staticmethod
    def for_view_name(view_name, cause=None):
        """
        Return a C{CannotFindViewException} instance with a helpful message
        built using the supplied C{view_name}.

        @param view_name: the name of the view that cannot be found.
        @param cause: the root cause, if any.
        @return: a C{CannotFindViewException} instance; never C{None}.
        """

        message = 'Cannot find the view named "{}"; did you map it?'.format(view_name)
        return CannotFindViewException(message, cause=cause)

    @staticmethod
    def for_missing_view_name(cause=None):
        """
        Return a C{CannotFindViewException} instance with a helpful message.

        @param cause: the root cause, if any.
        @return: a C{CannotFindViewException} instance; never C{None}.
        """

        message = 'No view name supplied.'
        return CannotFindViewException(message, cause=cause)


class SimpleMappingBasedViewResolver(object):
    # noinspection PyUnusedLocal
    def resolve_view(self, *args, **kwargs):
        view_name = kwargs[self.view_name_key]
        if view_name in self.view_mappings:
            view = self.view_mappings[view_name]
            if not view:
                raise CannotFindViewException(
                    'View for [{}] resolved to [None]; check configuration.'.format(view_name))
            return view
        elif has_text(view_name):
            raise CannotFindViewException.for_view_name(view_name)
        else:
            raise CannotFindViewException.for_missing_view_name(view_name)

    def __init__(self, view_mappings, view_name_key='view_name'):
        super(SimpleMappingBasedViewResolver, self).__init__()

        assert has_elements(view_mappings), 'The view mappings are required.'
        assert has_text(view_name_key), 'The view name key is required.'

        self.view_mappings = view_mappings
        self.view_name_key = view_name_key


class SimpleSuffixBasedViewResolver(object):
    """
    Resolve a logical view name to a (file)path by appending a suffix.

    Forex, the logical view name 'login' becomes 'login.html' with a suffix of '.html'.
    """

    # noinspection PyUnusedLocal
    def resolve_view(self, *args, **kwargs):
        """
        Resolve the logical view name to a (file)path by appending a suffix.

        @param args: ignored.
        @param kwargs: contains the logical view name.
        @return: the resolved (file)path.
        """

        if self.view_name_key in kwargs:
            logical_view_name = kwargs[self.view_name_key]
            if has_text(logical_view_name):
                view_name = '{}{}'.format(logical_view_name, self.suffix)
                return view_name
            else:
                raise CannotFindViewException.for_missing_view_name()
        else:
            raise CannotFindViewException(
                'No view name found in model using key [{}]; check configuration.'.format(self.view_name_key))

    def __init__(self, suffix='.html', view_name_key='view_name'):
        """
        Create a C{SimpleSuffixBasedViewResolver}.

        @param suffix: the suffix to be appended to the logical view name; must not be C{None}.
        @param view_name_key: the name of the logical view name in the model; must not be C{None}.
        """

        super(SimpleSuffixBasedViewResolver, self).__init__()

        assert has_text(suffix), 'The suffix is required.'
        assert has_text(view_name_key), 'The view name key is required.'

        self.suffix = suffix
        self.view_name_key = view_name_key
