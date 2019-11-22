<template>
  <div id="app">
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>

export default {
  name: 'app',
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}



.game-board {
  border: 5px cadetblue solid;

  width: 350px;
  margin: 0 auto;
}

.column {
  cursor: pointer;
}

.column rect.play:hover {
  fill-opacity: 0.75;
}

</style>
