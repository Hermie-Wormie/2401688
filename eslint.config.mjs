import security from "eslint-plugin-security";
import html from "eslint-plugin-html";

export default [
  {
    files: ["app/templates/**/*.html"],
    plugins: { security, html },
    rules: {
      ...security.configs.recommended.rules,
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: { document: "readonly" },
    },
  },
];