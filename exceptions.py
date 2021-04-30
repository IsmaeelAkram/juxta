class ArgsError(Exception):
    pass


class NoVoiceChannelError(Exception):
    pass


class AlreadyInVoiceChannelError(Exception):
    pass


class BotNotInVoiceChannelError(Exception):
    pass