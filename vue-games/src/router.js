import { createWebHistory, createRouter } from "vue-router";

import AnagramHunt from "./apps/AnagramHunt";
import MathFacts from "./apps/MathFacts";

const routes = [
  {
    path: '/anagram-hunt/',
    component: AnagramHunt,
    alias: ['/anagram-hunt']
  },
  {
    path: '/math-facts/',
    component: MathFacts,
    alias: ['/math-facts']
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});


export default router;
