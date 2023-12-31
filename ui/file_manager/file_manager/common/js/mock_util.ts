// Copyright 2021 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import {util} from './util.js';

/**
 * Mocks out the util.visitURL function and returns a restore function and a
 * function to interrogate the URL visitURL was invoked with.
 */
export function mockUtilVisitURL() {
  const oldVisitURL = util.visitURL;
  let visitedURL: string;
  util.visitURL = function(url: string) {
    visitedURL = url;
  };
  const getURL = () => {
    return visitedURL;
  };
  const restoreVisitURL = () => {
    util.visitURL = oldVisitURL;
  };
  return {getURL, restoreVisitURL};
}
