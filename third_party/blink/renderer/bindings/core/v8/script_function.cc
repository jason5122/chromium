// Copyright 2014 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "third_party/blink/renderer/bindings/core/v8/script_function.h"

#include "third_party/blink/renderer/platform/bindings/custom_wrappable.h"
#include "third_party/blink/renderer/platform/bindings/v8_binding.h"

namespace blink {

namespace {

class CallableHolder final : public CustomWrappable {
 public:
  static v8::Local<v8::Function> Create(ScriptState* script_state,
                                        ScriptFunction::Callable* callable) {
    CHECK(callable);
    CallableHolder* holder = MakeGarbageCollected<CallableHolder>(callable);
    // The wrapper is held alive by the CallHandlerInfo internally in V8 as long
    // as the function is alive.
    return v8::Function::New(script_state->GetContext(), CallCallback,
                             holder->Wrap(script_state), callable->Length(),
                             v8::ConstructorBehavior::kThrow)
        .ToLocalChecked();
  }

  static void CallCallback(const v8::FunctionCallbackInfo<v8::Value>& args) {
    RUNTIME_CALL_TIMER_SCOPE_DISABLED_BY_DEFAULT(args.GetIsolate(),
                                                 "Blink_CallCallback");
    v8::Local<v8::Object> data = v8::Local<v8::Object>::Cast(args.Data());
    auto* holder = static_cast<CallableHolder*>(ToCustomWrappable(data));
    ScriptState* script_state =
        ScriptState::From(args.GetIsolate()->GetCurrentContext());
    holder->callable_->CallRaw(script_state, args);
  }

  explicit CallableHolder(ScriptFunction::Callable* callable)
      : callable_(callable) {}
  const char* NameInHeapSnapshot() const final {
    return "ScriptFunction::Callable";
  }

  void Trace(Visitor* visitor) const override {
    visitor->Trace(callable_);
    CustomWrappable::Trace(visitor);
  }

 private:
  const Member<ScriptFunction::Callable> callable_;
};

}  // namespace

ScriptValue ScriptFunction::Callable::Call(ScriptState*, ScriptValue) {
  NOTREACHED();
  return ScriptValue();
}

void ScriptFunction::Callable::CallRaw(
    ScriptState* script_state,
    const v8::FunctionCallbackInfo<v8::Value>& args) {
  ScriptValue result =
      Call(script_state, ScriptValue(script_state->GetIsolate(), args[0]));
  V8SetReturnValue(args, result.V8Value());
}

v8::Local<v8::Function> ScriptFunction::BindToV8Function(
    ScriptState* script_state,
    Callable* callable) {
  return CallableHolder::Create(script_state, callable);
}

}  // namespace blink
