async function verifyUpgrade() {
    console.log("Starting verification...");
    try {
        const response = await fetch('http://localhost:8000/api/analyze-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: 'http://test-phish.net/login' })
        });

        console.log("Status:", response.status);
        const data = await response.json();

        console.log("\n--- Upgraded Response Format ---");
        console.log("Score:", data.score);
        console.log("Verdict:", data.verdict);
        console.log("Breakdown:", JSON.stringify(data.breakdown, null, 2));
        console.log("Reasons Count:", data.reasons?.length);
        console.log("Recommendations Count:", data.recommendations?.length);

        const expectedKeys = ['score', 'verdict', 'breakdown', 'reasons', 'recommendations'];
        const missingKeys = expectedKeys.filter(k => !(k in data));

        if (missingKeys.length === 0) {
            console.log("\nSUCCESS: All expected keys found in response.");
        } else {
            console.log("\nFAILURE: Missing keys:", missingKeys);
        }

    } catch (error) {
        console.error("Verification failed:", error.message);
    }
}

verifyUpgrade();
