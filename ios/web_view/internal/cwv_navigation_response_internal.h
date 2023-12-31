// Copyright 2023 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef IOS_WEB_VIEW_INTERNAL_CWV_NAVIGATION_RESPONSE_INTERNAL_H_
#define IOS_WEB_VIEW_INTERNAL_CWV_NAVIGATION_RESPONSE_INTERNAL_H_

#import "ios/web_view/public/cwv_navigation_response.h"

NS_ASSUME_NONNULL_BEGIN

@interface CWVNavigationResponse ()

- (nonnull instancetype)init NS_UNAVAILABLE;

- (nonnull instancetype)initWithResponse:(NSURLResponse*)response
                            forMainFrame:(BOOL)forMainFrame
    NS_DESIGNATED_INITIALIZER;

@end

NS_ASSUME_NONNULL_END

#endif  // IOS_WEB_VIEW_INTERNAL_CWV_NAVIGATION_RESPONSE_INTERNAL_H_
