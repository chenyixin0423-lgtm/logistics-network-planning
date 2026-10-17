<template>
  <main>
    <nav>
      <router-link to="/warehouseLocation">仓库选址</router-link>
      <router-link to="/routePlan">路径规划</router-link>
    </nav>
    <router-view />
  </main>
</template>

<style scoped>
nav { display: flex; gap: 24px; padding: 16px; }
</style>
