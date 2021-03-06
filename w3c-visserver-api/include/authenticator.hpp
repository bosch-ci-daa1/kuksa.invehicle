/*
 * ******************************************************************************
 * Copyright (c) 2018 Robert Bosch GmbH.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v2.0
 * which accompanies this distribution, and is available at
 * https://www.eclipse.org/org/documents/epl-2.0/index.php
 *
 *  Contributors:
 *      Robert Bosch GmbH - initial API and functionality
 * *****************************************************************************
 */
#ifndef __AUTHENTICATOR_H__
#define __AUTHENTICATOR_H__

#include <memory>
#include <string>

using namespace std;

class wschannel;
class vssdatabase;
class ILogger;

class authenticator {
 private:
  string pubkey = "secret";
  string algorithm = "RS256";
  std::shared_ptr<ILogger> logger;

  int validateToken(wschannel& channel, string authToken);

 public:
  authenticator(std::shared_ptr<ILogger> loggerUtil, string secretkey, string algorithm);
  int validate(wschannel &channel, vssdatabase *database,
               string authToken);
  
  void updatePubKey(string key);
  bool isStillValid(wschannel &channel);
  void resolvePermissions(wschannel &channel, vssdatabase *database);
};
#endif
