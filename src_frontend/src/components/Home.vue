<template>
  <div class="container">
    <img src="../assets/connect_ai.png">
    <h1>Welcome to Connect AI <span style="font-size: 20px">a Connect Four trainer</span></h1>
    <p>
      Everyone had this experience in their lifetime. Either you had a bet with your brother to get the bigger room or to win a bet against a friend. Normally these bets are fought with games. Card games, Chess or other games like Connect four. In life sometimes it’s crucial to win such a bet. But stay close, you don’t have to worry anymore about losing important games with our Software. Using new technologies such as Artificial Intelligence we create a Software that gives you at any moment the winning steps. Connect 4I does not only know long-known moves but also find new moves as the software is trained with each game. To reach this goal, we use already established algorithms and made them better.
    </p>
    <h3>What are you wating for? &#129300;</h3>
    <button @click="startGame" type="button" class="btn btn-danger">Start a game now</button>
  </div>

</template>

<script>


export default {
  name: 'Home',
  methods: {
    startGame(){
      this.axios.get('http://localhost:8080/api/game/start')
      .then((response) => {
        this.$router.push({
          name: 'Game',
          params: { id: response.data.id }
        })
      }).catch(error => {
        this.$swal("I couldn't create a new game!", `${error.response.status} - ${error.response.statusText}`, 'error');
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1 {
    margin-top: 20px;
  }
  h3 {
    margin: 40px 0 0;
    margin-bottom: 10px;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
</style>
