from nectarallocationclient import exceptions


def format_parameters(params, parse_semicolon=True):
    '''Reformat parameters into dict of format expected by the API.'''

    if not params:
        return {}

    if parse_semicolon:
        # expect multiple invocations of --parameters but fall back
        # to ; delimited if only one --parameters is specified
        if len(params) == 1:
            params = params[0].split(';')

    parameters = {}
    for p in params:
        try:
            (n, v) = p.split(('='), 1)
        except ValueError:
            msg = _('Malformed parameter(%s). Use the key=value format.') % p
            raise exceptions.CommandError(msg)

        if n not in parameters:
            parameters[n] = v
        else:
            if not isinstance(parameters[n], list):
                parameters[n] = [parameters[n]]
            parameters[n].append(v)

    return parameters
