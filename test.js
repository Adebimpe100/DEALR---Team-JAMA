import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const prompt = `
Return ONLY JSON.

{
  "materials": number,
  "labour": number,
  "overhead": number,
  "recommended_price": number,
  "floor_price": number
}

Job:
Tailor making Ankara dress
Fabric: 5000 NGN
Time: 6 hours
Skill: intermediate
`;
async function run() {
  const msg = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 500,
    messages: [
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  const raw = msg.content[0].text;
  console.log("RAW OUTPUT:\n", raw);

  try {
    const clean = raw.replace(/```json|```/g, "").trim();
    const data = JSON.parse(clean);
    console.log("✅ PARSED:", data);
  } catch (err) {
    console.error("❌ JSON FAILED:", err.message);
  }
}

run();