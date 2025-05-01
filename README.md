---
title: Cortex
emoji: 🐢
colorFrom: indigo
colorTo: gray
sdk: docker
pinned: false
license: afl-3.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# LLM Streaming API

This Space provides a FastAPI application that streams responses from the Cortex LLM model.

- Send GET requests to `/stream?task=<your_task>` to receive a streamed response from the model.
- Example: `/stream?task=make an agent which send mail by searching top 5 website from google`