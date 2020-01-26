const express = require('express');
const router = new express.Router();
//const knex = require('../db/knex')
const axios = require('axios')

router.get('/listPoints', function(req,res){
   knex('points')
   .select('*')
   .then(points=>{
    res.status(200).json({data: points, message: "success"});
   })
   .catch(err=>{
      res.status(500).json({err, message: "failed"});
   })
});

router.post('/deletePoint', function(req,res){
   knex('points')
   .where('id', req.body.point_id)
   .del()
   .then(()=>{
    res.status(200).json({message: "success"});
   })
   .catch(err=>{
      res.status(500).json({err, message: "failed"});
   });
})
  
module.exports = router;