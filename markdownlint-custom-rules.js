"use strict";

// Official names that are spelled with a hyphen and must not be changed.
const ALLOWED_NAMES = [
  "Center for Open-Source Research Software Advancement",
  "Open-Source @ Illinois",
];

// Replace a match with spaces of the same length, so column numbers stay correct.
const blank = (text) => " ".repeat(text.length);

module.exports = {
  names: ["no-hyphenated-open-source"],
  description: "Ensure 'open source' is not written as 'open-source'.",
  tags: ["wording", "consistency"],
  function: function noHyphenatedOpenSource(params, onError) {
    params.lines.forEach((line, index) => {
      const lineNumber = index + 1;

      // Ignore URLs, link targets, inline code, quoted examples, and allowed names.
      let masked = line
        .replace(/https?:\/\/[^\s)>\]]+/g, blank)
        .replace(/\]\([^)]*\)/g, blank)
        .replace(/`[^`]*`/g, blank)
        .replace(/"open-source"/gi, blank);
      for (const name of ALLOWED_NAMES) {
        masked = masked.split(name).join(blank(name));
      }

      const pattern = /\bopen-source\b/gi;
      let match;
      while ((match = pattern.exec(masked)) !== null) {
        onError({
          lineNumber: lineNumber,
          detail: "Use 'open source' instead of 'open-source'.",
          context: line.trim(),
          fixInfo: {
            editColumn: match.index + 1,
            deleteCount: match[0].length,
            insertText: line.substr(match.index, match[0].length).replace("-", " "),
          },
        });
      }
    });
  },
};
