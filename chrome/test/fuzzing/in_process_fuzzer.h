// Copyright 2023 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef CHROME_TEST_FUZZING_IN_PROCESS_FUZZER_H_
#define CHROME_TEST_FUZZING_IN_PROCESS_FUZZER_H_

#include <optional>

#include "chrome/test/base/in_process_browser_test.h"

// In-process fuzz test.
//
// This is equivalent to a browser test, in that the entire browser
// environment is available for your use, and you can do rich things that
// require the whole browser infrastructure.
//
// The 'Fuzz' method will be called repeatedly, and you just have to
// implement something sensible there to explore parts of Chrome's
// attack surface.
//
// Register your subclass with REGISTER_IN_PROCESS_FUZZER. There can only
// be one per executable.
//
// Different fuzz frameworks might run this in different ways.
// For instance,
// * libfuzzer runs this in a multi-process Chrome browser_test
//   environment.
// * centipede runs it in single-process browser_test mode (currently),
//   with an external fuzz co-ordinator running multiple instances
//   of Chrome.
// * in the future, snapshot fuzzers might pause a VM and resume
//   clones of it (to ensure a cleaner state for each iteration)
// To the extent possible, you should write your fuzzer to be
// implementation-independent and semantically express what
// should happen during such fuzzing of the whole browser.
class InProcessFuzzer : virtual public InProcessBrowserTest {
 public:
  // Called by the main function to create this class.
  // This is called prior to all the normal browser test setup,
  // so don't do anything important in your constructor.
  // Furthermore, this will be re-run even for child Chromium processes.
  InProcessFuzzer();
  ~InProcessFuzzer() override;

  // Called by the main function to run this fuzzer, after the browser_test
  // equivalent infrastructure has been set up.
  void Run(const std::vector<std::string>& libfuzzer_command_line);

  // If you override this, it's essential you call the superclass method.
  void SetUpOnMainThread() override;
  void RunTestOnMainThread() override;
  void TestBody() override {}

  friend int fuzz_callback(const uint8_t* data, size_t size);

  // Override if you want to pass particular command line arguments to
  // Chromium for its startup. This is called before any fuzz test case
  // is actually run, so unfortunately you can't generate these through
  // fuzzing. In addition, the browser test framework itself does all
  // sorts of fiddling with the arguments (e.g. a user data dir).
  // It's generally OK to leave this at the default unless you specifically
  // need to enable a feature or similar.
  // Do not include the executable name in your return value - that's
  // prepended automatically.
  virtual base::CommandLine::StringVector GetChromiumCommandLineArguments();

 protected:
  // Callback to actually do your fuzzing. This is called from the UI thread,
  // so you should take care not to block the thread too long. If you need
  // to run your fuzz case across multiple threads, consider a nested RunLoop.
  virtual int Fuzz(const uint8_t* data, size_t size) = 0;

 private:
  std::vector<std::string> libfuzzer_command_line_;
};

class InProcessFuzzerFactoryBase {
 public:
  virtual std::unique_ptr<InProcessFuzzer> CreateInProcessFuzzer() = 0;
};

extern InProcessFuzzerFactoryBase* g_in_process_fuzzer_factory;

// Class used to register a single in-process fuzzer in each executable.
template <typename T>
class InProcessFuzzerFactory : public InProcessFuzzerFactoryBase {
 public:
  InProcessFuzzerFactory() { g_in_process_fuzzer_factory = this; }
  std::unique_ptr<InProcessFuzzer> CreateInProcessFuzzer() override {
    return std::make_unique<T>();
  }
};

#define REGISTER_IN_PROCESS_FUZZER(fuzzer_class) \
  InProcessFuzzerFactory<fuzzer_class> fuzzer_instance;

#endif  // CHROME_TEST_FUZZING_IN_PROCESS_FUZZER_H_
