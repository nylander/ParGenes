#ifndef _OPENMP_IMPL_HPP_
#define _OPENMP_IMPL_HPP_

#include "../Command.hpp"

namespace MPIScheduler {

int getOpenMPThreads();

class OpenMPRanksAllocator: public RanksAllocator {
public:
  OpenMPRanksAllocator(const string &outputDir, const string &execPath); 
  virtual ~OpenMPRanksAllocator() {}
  virtual bool ranksAvailable() {return true;}
  virtual bool allRanksAvailable() {return true;}
  virtual InstancePtr allocateRanks(int requestedRanks, 
      CommandPtr command);
  virtual void freeRanks(InstancePtr instance) {}
  virtual vector<InstancePtr> checkFinishedInstances() {}
private:
  string _outputDir;
  string _execPath;
  Timer _globalTimer;
};


class OpenMPInstance: public Instance {
public:
  OpenMPInstance(const string &outputDir, 
      const string &execPath,
      int rank, 
      CommandPtr command);

  virtual ~OpenMPInstance() {}
  virtual bool execute(InstancePtr self);
  virtual void onFailure(int errorCode = 0);
private:
  string _execPath;
};


}
#endif