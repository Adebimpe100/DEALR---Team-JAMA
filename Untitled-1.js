
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const msg = await anthropic.messages.create({
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 1000,
  messages: [
    {
      role: "user",
      content: "Say hello in JSON format"
    }
  ]
});

console.log(msg.content[0].text);
