// Copyright 2020 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "android_webview/browser/tracing/background_tracing_field_trial.h"

#include <utility>

#include "components/tracing/common/background_tracing_utils.h"
#include "content/public/browser/background_tracing_config.h"
#include "content/public/browser/background_tracing_manager.h"
#include "services/tracing/public/cpp/tracing_features.h"

namespace {

using tracing::BackgroundTracingSetupMode;

const char kBackgroundTracingFieldTrial[] = "BackgroundWebviewTracing";

bool SetupBackgroundTracingFieldTrial(int allowed_modes) {
  auto tracing_mode = tracing::GetBackgroundTracingSetupMode();

  if (tracing_mode == BackgroundTracingSetupMode::kDisabledInvalidCommandLine) {
    return false;
  } else if (tracing_mode != BackgroundTracingSetupMode::kFromFieldTrial) {
    return tracing::SetupBackgroundTracingFromCommandLine(
        kBackgroundTracingFieldTrial);
  }

  auto& manager = content::BackgroundTracingManager::GetInstance();
  std::unique_ptr<content::BackgroundTracingConfig> config =
      manager.GetBackgroundTracingConfig(kBackgroundTracingFieldTrial);

  if (!config)
    return false;

  if ((config->tracing_mode() & allowed_modes) == 0)
    return false;

  // WebView-only tracing session has additional filtering of event names that
  // include package names as a privacy requirement (see
  // go/public-webview-trace-collection).
  config->SetPackageNameFilteringEnabled(
      config->tracing_mode() != content::BackgroundTracingConfig::SYSTEM);
  return manager.SetActiveScenario(
      std::move(config), content::BackgroundTracingManager::ANONYMIZE_DATA);
}

}  // namespace

namespace android_webview {

bool MaybeSetupSystemTracing() {
  if (!tracing::ShouldSetupSystemTracing())
    return false;

  return SetupBackgroundTracingFieldTrial(
      content::BackgroundTracingConfig::SYSTEM);
}

bool MaybeSetupWebViewOnlyTracing() {
  return SetupBackgroundTracingFieldTrial(
      content::BackgroundTracingConfig::PREEMPTIVE |
      content::BackgroundTracingConfig::REACTIVE);
}

}  // namespace android_webview
