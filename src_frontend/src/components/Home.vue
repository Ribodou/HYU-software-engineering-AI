<template>
  <div class="container">
    <img src="../assets/connect_ai.png">
    <h1>Welcome to Connect AI <span style="font-size: 20px">a Connect Four trainer</span></h1>
    <p>
      Everyone had this experience in their lifetime. Either you had a bet with your brother to get the bigger room or to win a bet against a friend. Normally these bets are fought with games. Card games, Chess or other games like Connect four. In life sometimes it’s crucial to win such a bet. But stay close, you don’t have to worry anymore about losing important games with our Software. Using new technologies such as Artificial Intelligence we create a Software that gives you at any moment the winning steps. Connect 4I does not only know long-known moves but also find new moves as the software is trained with each game. To reach this goal, we use already established algorithms and made them better.
    </p>
    <h3>What are you wating for? &#129300;</h3>
    Select the difficulty:  
    <select v-model="selected_difficulty" style="margin-left: 5px;">
      <option v-for="difficulty in difficulty_options" :key="`option-${difficulty}`" :value="difficulty">{{difficulty}}</option>
    </select>
    <br>
    <button @click="startGame" type="button" class="btn btn-danger" style="margin-top: 5px;">Start a game now</button>
    <br>
    <br>
    <h4>or</h4>
    <div >
      <form class="form-inline d-flex justify-content-center">
        <div class="form-group mr-1">
          <input style="width: 120px;" type="integer" v-model="olgGameId" class="form-control" id="text" placeholder="Game ID">
        </div>
        <button @click="loadOldGame" type="button" class="btn btn-success">Load and old game</button>
      </form>
    </div>
  </div>

</template>

<script>

export default {
  name: 'Home',
  data() {
      return {
          olgGameId: null,
          selected_difficulty: 'min-max',
          difficulty_options: [
            'random',
            'min-max',
            'alpha-zero'
          ]
      };
  },
  methods: {
    startGame(){
      this.axios.post('http://localhost:8080/api/game/start', { difficulty: this.selected_difficulty })
      .then((response) => {
        this.$router.push({
          name: 'Game',
          params: {
            id: response.data.id,
          }
        })
      }).catch(error => {
        this.$swal("I couldn't create a new game!", `${error.response.status} - ${error.response.statusText}`, 'error');
      })
    },
    loadOldGame(){
      if(parseInt(this.olgGameId) && parseInt(this.olgGameId) > 0 && parseInt(this.olgGameId) <= 1000000){
        this.$router.push({ name: 'Game', params:  {'id': this.olgGameId} })
      } else {
        this.$swal("The Game ID is not valid!", '', 'error');
      }
      
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
