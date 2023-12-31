// Copyright 2021 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef COMPONENTS_AUTOFILL_CONTENT_BROWSER_CONTENT_AUTOFILL_ROUTER_TEST_API_H_
#define COMPONENTS_AUTOFILL_CONTENT_BROWSER_CONTENT_AUTOFILL_ROUTER_TEST_API_H_

#include "base/memory/raw_ref.h"
#include "components/autofill/content/browser/content_autofill_router.h"

namespace autofill {

// Exposes some testing operations for ContentAutofillRouter.
class ContentAutofillRouterTestApi {
 public:
  explicit ContentAutofillRouterTestApi(ContentAutofillRouter* router)
      : router_(*router) {}

  void set_last_queried_source(ContentAutofillDriver* driver) {
    router_->last_queried_source_ = driver;
  }

  void set_last_queried_target(ContentAutofillDriver* driver) {
    router_->last_queried_target_ = driver;
  }

 private:
  const raw_ref<ContentAutofillRouter> router_;
};

inline ContentAutofillRouterTestApi test_api(ContentAutofillRouter& router) {
  return ContentAutofillRouterTestApi(&router);
}

}  // namespace autofill

#endif  // COMPONENTS_AUTOFILL_CONTENT_BROWSER_CONTENT_AUTOFILL_ROUTER_TEST_API_H_
