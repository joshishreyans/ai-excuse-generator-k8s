export async function generateExcuse(tone, days) {
  const res = await fetch("/api/excuse", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tone, days }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Failed to generate excuse");
  }

  return res.json();
}
