#!/usr/bin/env python
###########################################################################
###
### Licensed to the Apache Software Foundation (ASF) under one
### or more contributor license agreements.  See the NOTICE file
### distributed with this work for additional information
### regarding copyright ownership.  The ASF licenses this file
### to you under the Apache License, Version 2.0 (the
### "License"); you may not use this file except in compliance
### with the License.  You may obtain a copy of the License at
###
###     http://www.apache.org/licenses/LICENSE-2.0
###
### Unless required by applicable law or agreed to in writing,
### software distributed under the License is distributed on an
### "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
### KIND, either express or implied.  See the License for the
### specific language governing permissions and limitations
### under the License.
###########################################################################
###                           B U I L D B O T                           ###
###########################################################################
### this script runs on all the buildbot vms and it started with the vm ###
### it does several functions:                                          ###
### 1) clean build directories                                          ###
### 2) update source directories from git                               ###
### 3) generate build environment with cmake                            ###
### 4) build binaries and make logs                                     ###
### 5) commit binaries and log to git                                   ###
### 6) run test suite and build log                                     ###
###########################################################################
import json



# -------------------------
# -----   S E T U P   -----
def setup() :
### Load build.json, and change working directory
    global buildConfig

    jsFile = open('build.json')
    buildConfig = json.load(jsFile)



global buildConfig
print('jan var her')
setup()
print(buildConfig)
print('jan igen')
exit(1)



# ---------------------------------------------------
# --------   S C H E D U L E R   C L A S S   --------
class schedulerClass(object) :
### Class to hold information about the active tasks ###
    def __init__(self):
        # set cycle time so big, that it will be corrected
        self.schedules   = []
        self.funcs       = {}
        self.cycleTime   = 1
        self.lastRun     = 0
        self.countScript = 0



    def addFunction(self, func) :
        self.funcs[func.func_name] = func



    def addSchedule(self, name, metrics, cycle, url, script):
        cmd = script['cmd']
        self.schedules.append({'name'      : name            , 'metrics' : metrics,
                               'cycle'     : int(cycle)      , 'nextcycle' : 0,
                               'last_send' : 0,
                               'url'       : url,
                               'cmd'       : self.funcs[cmd],
                               'params'    : script})

    def runCycle(self):
    # loop through all function and execute those whose time has come
        loopTime  = int(time.time())
        if loopTime > self.lastRun +5:
          print("SKIPPED " + str(loopTime - self.lastRun) + " seconds")
        if loopTime > self.lastRun +300:
          print("Looping did " + str(self.countScript) + " scripts")
          self.countScript = 0
        self.lastRun = loopTime

        for i in self.schedules :
          # time to activate function ?
          if i['nextcycle'] <= loopTime :
            #debug print i['cmd'].func_name + " with name(" + i['name'] + ")\n"
            i['cmd'](i['name'], i['params'], i['metrics'], not cfg.developPlatform)
            self.countScript += 1
            # calculate new cycle time
            if i['nextcycle'] > 0 :
              i['nextcycle'] += i['cycle']
            else :
              iX   = 1 # int(time.time())
              i['nextcycle'] = iX + i['cycle'] - (iX % i['cycle'])

          # send metric to circonus, independent of function call
          if i['metrics'] != {} and i['last_send'] < loopTime - 60:
            # cfg.set_metric(i['url'], i['metrics'])
            i['last_send'] = loopTime
sched = schedulerClass()



# -----------------------------------------------------
# --------   H E L P E R   F U N C T I O N S   --------
def addToWhiteList(func):
### this function add func to the white list of callable functions
    global sched

    # pass function to scheduler
    sched.addFunction(func)
    return func



def runScript(cmd) :
### this function runs a script with redirect of stdout, stderr
    return os.system(cmd + " > /dev/null 2>&1")



def daemonize() :
### this function forks on linux to start as daemon
    if cfg.developPlatform :
      print("Cannot run as daemon")
      return

    if os.fork() != 0 :
      exit(1)

    # child
    log_file   = open("/var/log/brokercontroller.log", 'w')
    sys.stdout = log_file
    sys.stderr = log_file



# ---------------------------------------------------------
# --------   I N F R A B O T   F U N C T I O N S   --------
def infrabot_maint(channel, id, window, msg) :
### put host/service in maintenance

    # TBD JANI


    # locate alert.
    #for i in alert.alertTree :
    #  x = alert.alertTree[i]
    #  if id == x['name'] :
    #    cfg.update_status('/maintenance',  {'stop': window,
    #                                        'item': x['_cid'] })
    #    x['maintenance'] = True
    #    alert.build_alert_list_from_circonus()
    #    return True, ""
    return "infrabot_maint"



def infrabot_ack(channel, id, msg) :
### acknowledge alert

    # TBD msg.

    # locate alert.
    #for i in alert.alertTree :
    #  x = alert.alertTree[i]
    #  if id == x['name'] :
    #    cfg.update_status('/acknowledgement',  {'acknowledged_until': window,
    #                                            'alert':              x['_cid'] })
    #    x['acknowledged'] = True
    #    alert.build_alert_list_from_circonus()
    #    return True, ""
    return "infrabot_ack"



def infrabot_cancel(channel, id) :
### send new alerts to infrabot
    #for i in alert.alertTree :
    #  x = alert.alertTree[i]
    #  if id == 'all' :
    #    alert.sendToInfrabot(x)
    #  elif id == 'open' :
    #    if not x['cleared'] :
    #      alert.sendToInfrabot(x)
    #  elif id == 'active' :
    #    if not x['maintenance'] and not x['acknowledged'] and not x['cleared'] :
    #      alert.sendToInfrabot(x)
    #  elif id == x['name'] :
    #    alert.sendToInfrabot(x)

    return "infrabot_cancel"



def infrabot_show(channel, id) :
### send configuration to infrabot

    #TBD JANI
    return "infrabot_show"



# -------------------------------------------------------
# --------   H A N D L E R   F U N C T I O N S   --------
@addToWhiteList
def run_updateAlert(name, params, metric, useScript) :
### update alert.json
    alert.build_alert_list_from_circonus()



@addToWhiteList
def run_CommsCheck(name, params, metric, useScript) :
### update alert.json
    # check for new http trap alerts
    alert.update_alert_list_from_httptrap()

    # TBD JAN (send new alert changes to infrabot)

    # check for new connections or command to execute
    cmd = alert.check_socket()
    if not cmd is None :
      # last sent will always be True
      if not cmd['cmd'] == 'keepalive' :
        print(str(cmd))

      cmd['result'] = True
      # check for handling
      if cmd['cmd'] == 'init' :
        # internal command to signal connection from asfbot plugin
        alert.build_alert_list_from_circonus()
        return
      elif cmd['cmd'] == 'keepalive' :
        # keepalive command
        cmd['msg'] = ''
      elif cmd['cmd'] == 'maint' :
        # maintenance command
        cmd['msg'] = infrabot_maint(cmd['channel'], cmd['id'], cmd['time'], cmd['msg'])
      elif cmd['cmd'] == 'ack' :
        # acknowledge command
        cmd['msg'] = infrabot_ack(cmd['channel'], cmd['id'], cmd['msg'])
      elif cmd['cmd'] == 'cancel' :
        # cancel command
        cmd['msg'] = infrabot_cancel(cmd['channel'], cmd['id'])
      elif cmd['cmd'] == 'show' :
        # list command
        cmd['msg'] = infrabot_show(cmd['channel'], cmd['id'])
      else :
        # unknown command
        cmd['msg']   = "INTERNAL ERROR, brokerController received unknown json object\n"

      alert.send_socket(cmd)



@addToWhiteList
def run_fail2ban(name, params, metric, useScript) :
### Check that fail2ban works
    # TBD JAN
    # print "running " + name
    metric['rc'] = 111



@addToWhiteList
def run_jira(name, params, metric, useScript) :
### Check that jira works
    # TBD JAN
    # print "running " + name
    metric['rc'] = 112
    metric['new_tickets'] = 100
    metric['open_tickets'] = 200
    metric['solved_tickets'] = 1



@addToWhiteList
def run_rsync(name, params, metric, useScript) :
### Check that rsync works
    if useScript :
      metric['rc'] = runScript('check_rsyncd.pl ' + params['name'])
    else :     
      metric['rc'] = 113

@addToWhiteList
def run_ldap(name, params, metric, useScript) :
### Check that ldap works
    if useScript :
      metric['rc'] = runScript('check_ldap.sh ldaps://' + params['name'] + '.apache.org:636')
    else :     
      metric['rc'] = 113
    


@addToWhiteList
def run_ldap_sync(name, params, metric, useScript) :
### Check that ldap synchronizes
    if useScript :
      metric['rc'] = runScript('check_ldap_sync.sh ' + params['name'] + '.apache.org')
    else :     
      metric['rc'] = 114



@addToWhiteList
### send alive signal to circonus
def run_mon(name, params, metric, useScript) :
    metric['rc'] = 1



@addToWhiteList
### Check that svn synchronizes around the globe
def run_svn_sync(name, params, metric, useScript) :
    if useScript :
      metric['rc'] = runScript('check_svn_replication.sh ' + params['url1'] + ' ' + params['url2'])
    else :     
      metric['rc'] = 116



@addToWhiteList
### Check that viewvc console is available
def run_viewvc(name, params, metric, useScript) :
    # print "running " + name
    # TBD JAN
    metric['rc'] = 117



# ---------------------------------
# -----   H O U S E H O L D   -----
def household(sched) :
### Load httptrap checks from circonus (checks we handle in this program)
    global ALERT_SCHEDULE, COMMS_SCHEDULE, ASFINFRA_DELAY

    print("--> loading circonus.json (map of configuration) and alerts.json (status)")
    alert.setup([0, ASFINFRA_DELAY_1, ASFINFRA_DELAY_2, ASFINFRA_DELAY_3, ASFINFRA_DELAY_4, ASFINFRA_DELAY_5])

    print("--> loading /check_bundle from circonus (current configuration)")
    circCfg = cfg.get_set_of_cfg(['/check_bundle'])

    # add local check, NON configurable
    sched.addSchedule('ALERTS update', {}, ALERT_SCHEDULE, '', {'cmd' : 'run_updateAlert'})
    sched.addSchedule('Comms check',   {}, COMMS_SCHEDULE, '', {'cmd' : 'run_CommsCheck'})

    # find all checks to be handled locally
    for i in circCfg['/check_bundle'] :
       # httptrap is handled by this module
       if i['type'] == 'httptrap' :
         script = eval(i['notes'])
         if not script['cmd'] == 'none' :
           resultMetric = {}
           for j in i['metrics'] :
             resultMetric[j['name']] = 0
             sched.addSchedule(i['display_name'],
                              resultMetric, 
                              script['cycle'],
                              i['config']['submission_url'],
                              script)



# ---------------------------------
# ----------   M A I N   ----------
if __name__ == '__main__':
  # constants used
  ALERT_SCHEDULE = 300
  COMMS_SCHEDULE = 1
  ASFINFRA_DELAY_1 =   300
  ASFINFRA_DELAY_2 =   600
  ASFINFRA_DELAY_3 =  1800
  ASFINFRA_DELAY_4 =  3600
  ASFINFRA_DELAY_5 = 10800

  # start daemon on linux
  daemonize()
  print('Circonus private broker extension, version 0.6')

  print('-> Starting')
  household(sched)

  print('-> Loop')
  while True :
    sched.runCycle()
    sys.stdout.flush()
    time.sleep(sched.cycleTime)

  print('-> exiting')

