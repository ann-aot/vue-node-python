import cypress from "eslint-plugin-cypress";

export default [
    {
        files: ["cypress/**/*.js"],
        languageOptions: {
            ecmaVersion: 2021,
            sourceType: "module",
            globals: {
                cy: "readonly",
                Cypress: "readonly"
            }
        },
        plugins: {
            cypress
        },
        rules: {
            "cypress/no-assigning-return-values": "error",
            "cypress/no-unnecessary-waiting": "warn"
        }
    }
];
