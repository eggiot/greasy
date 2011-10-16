import pygame

class SoundHandler():
    def __init__(self, channels=8):
        pygame.mixer.init()
        self.backgroundChannel = pygame.mixer.find_channel()
        self.backgroundMusic = None
        self.currentSounds = {}
        self.numChannels = channels
        pygame.mixer.set_num_channels(channels)
    
    def testChannels(self, increase=1):
        """
        Test if all the channels are active, optionally increasing the number of
        channels if they are all active.
        """
        if pygame.mixer.get_num_channels() == self.numChannels:
            if increase != 0:
                pygame.mixer.set_num_channels(self.numChannels + increase)
            return True
        else:
            return False
    
    def loadSound(self, filename):
        """
        Return a pygame sound
        """
        return pygame.mixer.Sound(filename)
    
    def playSound(self, filename, channel=None, loops=0, save=True, test=True):
        """
        Play a sound on a new channel or on an existing channel if the sound has been played before
        """
        if not channel:
            if filename in self.currentSounds:
                channel = self.currentSounds[filename]
            else:
                if test:
                    self.testChannels()
                    channel = pygame.mixer.find_channel()
                else:
                    channel = pygame.mixer.find_channel()
        try:
            currentSound = self.loadSound(filename)
        except pygame.error:
            currentSound = filename
        try:
            channel.play(currentSound, loops)
        except TypeError:
            print "Error playing sound. File is of type ", type(currentSound)
            return None
        if save:
            self.currentSounds[filename] = channel
    def loopSound(self, filename, channel=None, loops=-1, save=True):
        """
        Loop a sound a specified number of times
        """
        self.playSound(filename, channel, loops, save)
    
    def stopSound(self, filename, remove=True, channel=None):
        """
        Stop playback of a sound
        """
        if not channel:
            try:
                channel = self.currentSounds[filename]
            except KeyError:
                print str(filename), "is not playing."
                return None
        channel.stop()
        if remove:
            del self.currentSounds[filename]
    
    def pauseSound(self, filename, channel=None):
        """
        Pause playback of a sound
        """
        if not channel:
            try:
                channel = self.currentSounds[filename]
            except KeyError:
                print str(filename), "has not been loaded,"
                return None
        channel.pause()
    
    def resumeSound(self, filename, channel=None):
        if not channel:
            try:
                channel = self.currentSounds[filename]
            except KeyError:
                print str(filename), "has not been loaded"
                return None
        channel.unpause()
    
    def fadeout(self, time, secs=True):
        """
        Fadeout playback of sound over specified period of time
        """
        if secs:
            pygame.mixer.fadeout(time*1000)
        else:
            pygame.mixer.fadeout(time)
        
    ##### BACKGROUND MUSIC #####
    def loadBackgroundMusic(self, filename):
        self.backgroundMusic = self.loadSound(filename)
    
    def playBackgroundMusic(self, filename=None):
        """
        play background music on dedicated background channel
        """
        if filename or self.backgroundMusic:
            self.loadBackgroundMusic(filename)
        try:
            self.playSound(self.backgroundMusic, channel=self.backgroundChannel, save=False)
        except TypeError:
            print "Error playing background music. File is of type ", type(self.backgroundMusic)
    
    def loopBackgroundMusic(self, filename=None, loops=-1):
        """
        loop playback of background music on dedicated background channel
        """
        if filename or self.backgroundMusic:
            self.loadBackgroundMusic(filename)
        self.loopSound(self.backgroundMusic, channel=self.backgroundChannel, loops=loops, save=False)
    
    def stopBackgroundMusic(self):
        self.backgroundChannel.stop()
    
    def pauseBackgroundMusic(self):
        self.backgroundChannel.pause()
    
    def resumeBackgroundMusic(self):
        self.backgroundChannel.unpause()