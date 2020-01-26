const express = require('express');
const router = new express.Router();
const knex = require('../db/knex')

router.get('/listPoints', function(req,res){
   console.log('i got called')
   knex('points')
   .select('*')
   .then(points=>{
      let toReply = [];
      for(let i=0; i<points.length; i++){
         toReply.push({
            latitude: points[i].lat,
            longitude: points[i].lon,
            title: points[i].event_name,
            description: points[i].description,
            image: points[i].image
         })
      }
    res.status(200).json({data: toReply, message: "success"});
   })
   .catch(err=>{
      console.log(err)
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