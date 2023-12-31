// Copyright 2021 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "services/device/public/cpp/test/fake_device_posture_provider.h"

#include <memory>
#include <utility>

namespace device {

FakeDevicePostureProvider::FakeDevicePostureProvider() = default;

FakeDevicePostureProvider::~FakeDevicePostureProvider() = default;

void FakeDevicePostureProvider::Bind(
    mojo::PendingReceiver<mojom::DevicePostureProvider> receiver) {
  receivers_.Add(this, std::move(receiver));
}

void FakeDevicePostureProvider::AddListenerAndGetCurrentPosture(
    mojo::PendingRemote<mojom::DevicePostureClient> client,
    AddListenerAndGetCurrentPostureCallback callback) {
  posture_clients_.Add(std::move(client));
  std::move(callback).Run(current_posture_);
}

void FakeDevicePostureProvider::AddListenerAndGetCurrentViewportSegments(
    mojo::PendingRemote<mojom::DeviceViewportSegmentsClient> client,
    AddListenerAndGetCurrentViewportSegmentsCallback callback) {
  viewport_segment_clients_.Add(std::move(client));
  std::move(callback).Run(current_viewport_segments_);
}

void FakeDevicePostureProvider::SetCurrentPostureForTesting(
    device::mojom::DevicePostureType posture) {
  current_posture_ = posture;
  DispatchPostureChanges();
}

void FakeDevicePostureProvider::DispatchPostureChanges() {
  for (auto& client : posture_clients_) {
    client->OnPostureChanged(current_posture_);
  }
}

}  // namespace device
