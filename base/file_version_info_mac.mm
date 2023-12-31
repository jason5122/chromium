// Copyright 2012 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "base/file_version_info_mac.h"

#import <Foundation/Foundation.h>

#include "base/apple/bridging.h"
#include "base/apple/bundle_locations.h"
#include "base/files/file_path.h"
#include "base/mac/foundation_util.h"
#include "base/strings/sys_string_conversions.h"
#include "build/build_config.h"

FileVersionInfoMac::FileVersionInfoMac(NSBundle* bundle) : bundle_(bundle) {}

FileVersionInfoMac::~FileVersionInfoMac() = default;

// static
std::unique_ptr<FileVersionInfo>
FileVersionInfo::CreateFileVersionInfoForCurrentModule() {
  return CreateFileVersionInfo(base::apple::FrameworkBundlePath());
}

// static
std::unique_ptr<FileVersionInfo> FileVersionInfo::CreateFileVersionInfo(
    const base::FilePath& file_path) {
  NSString* path = base::SysUTF8ToNSString(file_path.value());
  NSBundle* bundle = [NSBundle bundleWithPath:path];
  return std::make_unique<FileVersionInfoMac>(bundle);
}

std::u16string FileVersionInfoMac::company_name() {
  return std::u16string();
}

std::u16string FileVersionInfoMac::company_short_name() {
  return std::u16string();
}

std::u16string FileVersionInfoMac::internal_name() {
  return std::u16string();
}

std::u16string FileVersionInfoMac::product_name() {
  return GetString16Value(kCFBundleNameKey);
}

std::u16string FileVersionInfoMac::product_short_name() {
  return GetString16Value(kCFBundleNameKey);
}

std::u16string FileVersionInfoMac::product_version() {
  // On macOS, CFBundleVersion is used by LaunchServices, and must follow
  // specific formatting rules, so the four-part Chrome version is in
  // CFBundleShortVersionString. On iOS, both have a policy-enforced limit
  // of three version components, so the full version is stored in a custom
  // key (CrBundleVersion) falling back to CFBundleVersion if not present.
#if BUILDFLAG(IS_IOS)
  std::u16string version(GetString16Value(CFSTR("CrBundleVersion")));
  if (version.length() > 0)
    return version;
  return GetString16Value(CFSTR("CFBundleVersion"));
#else
  return GetString16Value(CFSTR("CFBundleShortVersionString"));
#endif  // BUILDFLAG(IS_IOS)
}

std::u16string FileVersionInfoMac::file_description() {
  return std::u16string();
}

std::u16string FileVersionInfoMac::file_version() {
  return product_version();
}

std::u16string FileVersionInfoMac::original_filename() {
  return GetString16Value(kCFBundleNameKey);
}

std::u16string FileVersionInfoMac::special_build() {
  return std::u16string();
}

std::u16string FileVersionInfoMac::GetString16Value(CFStringRef name) {
  if (bundle_) {
    NSString* ns_name = base::apple::CFToNSPtrCast(name);
    NSString* value = [bundle_ objectForInfoDictionaryKey:ns_name];
    if (value) {
      return base::SysNSStringToUTF16(value);
    }
  }
  return std::u16string();
}
