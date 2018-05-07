class VersionMismatch(Exception):
    def __init__(self, version, minv, maxv):
        self.message = "Version %s outside of supported %s - %s range" % (version, minv, maxv)

    def __str__(self):
        return self.message
