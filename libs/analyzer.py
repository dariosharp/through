import lief, os
import platform
import subprocess
from libs.findfunctioninlib import FindFunctionInLibs


class Analyzer:
    def __init__(self, pathbinary, function, pathlibraries, pathida):
        self.binary = lief.parse(pathbinary)
        self.function = function
        parsedpathlibraries = self.parsepath(pathlibraries)
        self.libraries = ["{}{}".format(parsedpathlibraries,l) for l in self.binary.libraries]
        self.pathida = pathida
    def getLibs(self):
        return [l for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]
    def getFunctions(self):
        return [f for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib] 
    def getFunctionPerLib(self):
        return [(f,l) for list_per_lib in FindFunctionInLibs(self.libraries,self.function) for f,l in list_per_lib]
    def parsepath(self,pathlibraries):
        if platform.system() == "Windows" and pathlibraries[-1] != "\\":
            return "{}\\".format(pathlibraries)
        if platform.system() == "Linux" and pathlibraries[-1] != "/":
            return "{}/".format(pathlibraries)
        return pathlibraries
    def genIDB(self, lib):
        command = [
            "{}\\{}".format(self.pathida,"idat.exe"),
            "-B",
            "-A",
            lib]
        print(command)
        process = subprocess.Popen(command)
        process.wait()
        return process.returncode
    def execplugin(self, idb, plugin, *args):
        path2subplugin = "{}\\{}".format(self.pathida,"plugins\\subplugin")
        #subprocess.call("rm {}.logs".format(idb))
        command = [
            "{}\\idat.exe".format(self.pathida),
            "-S\"{}\\{} {}\"".format(path2subplugin, plugin, " ".join(args)),
            "-L\"{}.logs\"".format(idb),
            "-A",
            idb]
        command = ' '.join(command)
        print(command)
        subprocess.call(command)
    def getResults(self, idb):
        print("{}.logs".format(idb))
        with open("{}.logs".format(idb), "r") as file:
            data = file.read()
        plugininfo = False
        prow = []
        for row in data.split():
            if plugininfo == True:
                if row == "*****PLUGIN-END*****":
                    return prow
                prow = prow + [row]
            if row == "*****PLUGIN-START*****":
                plugininfo = True
        return None





