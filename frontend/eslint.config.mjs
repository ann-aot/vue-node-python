// eslint.config.mjs
import vue from 'eslint-plugin-vue';
import typescript from '@typescript-eslint/eslint-plugin';
import parser from '@typescript-eslint/parser';
import vueParser from 'vue-eslint-parser';
import prettier from 'eslint-plugin-prettier';

export default [
  {
    files: ['**/*.ts', '**/*.vue', '**/*.js'],
    ignores:['**/node_modules/**', '**/dist/**', '**/build/**'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        parser: {
          ts: parser,
        },
        extraFileExtensions: ['.vue'],
      },
    },
    plugins: {
      vue,
      '@typescript-eslint': typescript,
      prettier
    },
    rules: {

      // TypeScript rules
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-explicit-any': 'warn',

      // General rules
      'no-console': 'error',
      'no-debugger': 'error',
      // Prettier integration
      'prettier/prettier': 'error', 

    },
  },
];
