---
name: ruby-llm-usage
description: >
  Guidance on how to correctly use the internal ruby_llm and llm_json gems. 
  Trigger this skill whenever the user asks to write, fix, or update code that interacts with ruby_llm, llm_json, or LLM services in Ruby.
---

# ruby_llm & llm_json Usage Guide

## Overview
`ruby_llm` and `llm_json` are internal, private Ruby libraries. **DO NOT GUESS OR HALLUCINATE THEIR APIs.** They do not follow the conventions of public libraries like `instructor`, `ruby-openai`, or `ActiveModel`.

## API Documentation

### 1. ruby_llm
This library is responsible for sending requests to LLM providers.

**Correct Initialization:**
```ruby
require 'ruby_llm'
# You MUST instantiate the service explicitly with a profile name.
@llm = RubyLLM::LLMService.new(profile_name: 'glm') # or 'default', etc.
```

**Correct Call:**
```ruby
messages = [
  { role: 'system', content: "..." },
  { role: 'user', content: "..." }
]
response = @llm.call_with_messages(messages: messages, temperature: 0.1)
# The raw string is accessed via response.content
raw_text = response.content
```

### 2. llm_json
This library is **strictly a parser** for recovering broken JSON from LLMs. It DOES NOT provide structured output generation (like `attribute :foo`), nor does it have a `Model` module.

**Correct Parsing:**
```ruby
require 'llm_json'
# It acts as a drop-in replacement for JSON.parse
parsed_hash = LLMJSON.parse(raw_text)
```

## Workflow for Structured Output
If you need an LLM to return a structured JSON object:
1. Append the desired JSON schema constraints manually to your `system` prompt.
2. Make a standard `@llm.call_with_messages` request.
3. Parse `response.content` using `LLMJSON.parse`.

## Common Mistakes (Anti-Patterns)
- **DO NOT** use `LlmJson::Model` or `LLMJSON::Model`. They do not exist.
- **DO NOT** use `LLMJSON.generate(SomeClass, messages: messages)`.
- **DO NOT** assume `RubyLLM` automatically reads `llm.yml` globally without initialization. You must call `RubyLLM::LLMService.new(profile_name: '...')`.
