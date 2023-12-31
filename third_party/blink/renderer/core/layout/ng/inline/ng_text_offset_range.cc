// Copyright 2020 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "third_party/blink/renderer/core/layout/ng/inline/ng_text_offset_range.h"

#include <ostream>

namespace blink {

std::ostream& operator<<(std::ostream& ostream,
                         const NGTextOffsetRange& offset) {
  return ostream << "{" << offset.start << ", " << offset.end << "}";
}

}  // namespace blink
