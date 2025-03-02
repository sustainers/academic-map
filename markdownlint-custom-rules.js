"use strict";

module.exports = {
  names: ["no-hyphenated-open-source"],
  description: "Ensure 'open source' is not written as 'open-source'.",
  tags: ["wording", "consistency"],
  function: function noHyphenatedOpenSource(params, onError) {
    params.lines.forEach((line, index) => {
      const lineNumber = index + 1;
      const match = line.match(/\b open-source \b/); // Find "open-source"

      if (match) {
        onError({
          lineNumber: lineNumber,
          detail: "Use 'open source' instead of 'open-source'.",
          context: line.trim(), // Provide surrounding text
          fixInfo: {
            editColumn: match.index + 1, // Position in the line
            deleteCount: match[0].length,
            insertText: " open source ",
          },
        });
      }
    });
  },
};
