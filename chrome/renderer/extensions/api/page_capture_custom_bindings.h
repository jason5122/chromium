// Copyright 2012 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef CHROME_RENDERER_EXTENSIONS_API_PAGE_CAPTURE_CUSTOM_BINDINGS_H_
#define CHROME_RENDERER_EXTENSIONS_API_PAGE_CAPTURE_CUSTOM_BINDINGS_H_

#include "extensions/renderer/object_backed_native_handler.h"

namespace extensions {
class IPCMessageSender;

// Implements custom bindings for the pageCapture API.
class PageCaptureCustomBindings : public ObjectBackedNativeHandler {
 public:
  PageCaptureCustomBindings(ScriptContext* context,
                            IPCMessageSender* ipc_message_sender);

  // ObjectBackedNativeHandler:
  void AddRoutes() override;

 private:
  // Creates a Blob with the content of the specified file.
  void CreateBlob(const v8::FunctionCallbackInfo<v8::Value>& args);
  void SendResponseAck(const v8::FunctionCallbackInfo<v8::Value>& args);

  // The IPCMessageSender for this context. Must outlive this class.
  IPCMessageSender* const ipc_message_sender_;
};

}  // namespace extensions

#endif  // CHROME_RENDERER_EXTENSIONS_API_PAGE_CAPTURE_CUSTOM_BINDINGS_H_
