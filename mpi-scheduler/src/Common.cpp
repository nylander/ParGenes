#include "Common.hpp"
#include<iostream>

#include <stdio.h>
#include <ftw.h>
#include <unistd.h>

namespace MPIScheduler {

int unlink_cb(const char *fpath, const struct stat *sb, int typeflag, struct FTW *ftwbuf)
{
  int rv = remove(fpath);
  if (rv)
    perror(fpath);
  return rv;
}

string Common::getIncrementalLogFile(const string &path, 
      const string &name,
      const string &extension)
{
  string file = joinPaths(path, name + "." + extension);
  int index = 1;
  while (ifstream(file).good()) {
    file = joinPaths(path, name + "_" + to_string(index) + "." + extension);
    index++;
  }
  return file;
}

int Common::systemCall(const string &command, const string &outputFile)
{
  int result = 0;
  FILE *ptr, *file;
  file = fopen(outputFile.c_str(), "w");
  if ((ptr = popen(command.c_str(), "r")) != NULL) {
    char buf[BUFSIZ];
    while (fgets(buf, BUFSIZ, ptr) != NULL) {
      fprintf(file, "%s", buf);
    }
    result = pclose(ptr);
  }
  fclose(file);
  return result;
}

} // namespace MPIScheduler

