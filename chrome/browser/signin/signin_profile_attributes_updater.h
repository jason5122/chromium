// Copyright 2018 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef CHROME_BROWSER_SIGNIN_SIGNIN_PROFILE_ATTRIBUTES_UPDATER_H_
#define CHROME_BROWSER_SIGNIN_SIGNIN_PROFILE_ATTRIBUTES_UPDATER_H_

#include "base/files/file_path.h"
#include "base/memory/raw_ptr.h"
#include "base/scoped_observation.h"
#include "components/keyed_service/core/keyed_service.h"
#include "components/prefs/pref_service.h"
#include "components/signin/public/identity_manager/identity_manager.h"

class ProfileAttributesStorage;

// This class listens to various signin events and updates the signin-related
// fields of ProfileAttributes.
class SigninProfileAttributesUpdater
    : public KeyedService,
      public signin::IdentityManager::Observer {
 public:
  SigninProfileAttributesUpdater(
      signin::IdentityManager* identity_manager,
      ProfileAttributesStorage* profile_attributes_storage,
      const base::FilePath& profile_path,
      PrefService* prefs);

  SigninProfileAttributesUpdater(const SigninProfileAttributesUpdater&) =
      delete;
  SigninProfileAttributesUpdater& operator=(
      const SigninProfileAttributesUpdater&) = delete;

  ~SigninProfileAttributesUpdater() override;

 private:
  // KeyedService:
  void Shutdown() override;

  // Updates the profile attributes on signin and signout events.
  void UpdateProfileAttributes();

  // IdentityManager::Observer:
  void OnPrimaryAccountChanged(
      const signin::PrimaryAccountChangeEvent& event) override;

  // This dangling raw_ptr occurred in:
  // unit_tests: All/IsolatedWebAppReaderRegistryFactoryTest.GuardedBehindFeatureFlag/1
  // https://ci.chromium.org/ui/p/chromium/builders/try/win-rel/237392/test-results?q=ExactID%3Aninja%3A%2F%2Fchrome%2Ftest%3Aunit_tests%2FIsolatedWebAppReaderRegistryFactoryTest.GuardedBehindFeatureFlag%2FAll.1+VHash%3Ad3d9eb66b4bd136c
  raw_ptr<signin::IdentityManager, FlakyDanglingUntriaged> identity_manager_;
  raw_ptr<ProfileAttributesStorage> profile_attributes_storage_;
  const base::FilePath profile_path_;
  raw_ptr<PrefService> prefs_;
  base::ScopedObservation<signin::IdentityManager,
                          signin::IdentityManager::Observer>
      identity_manager_observation_{this};
};

#endif  // CHROME_BROWSER_SIGNIN_SIGNIN_PROFILE_ATTRIBUTES_UPDATER_H_
