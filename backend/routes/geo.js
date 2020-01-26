const express = require('express');
const router = new express.Router();
//const knex = require('../db/knex')
const axios = require('axios')

router.post('/popSong', function(req,res){
   console.log('hello');
   res.status(200).json({message: "success"});
})
  
module.exports = router;