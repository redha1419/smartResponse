import React, {useState} from 'react';
import { StyleSheet, Text, View, ImageBackground} from 'react-native';
import { Button } from 'react-native-elements';

export default class Welcome extends React.Component {
  render(){
    return (
      <View style={{}}>

      <ImageBackground
          style = {{width:375, height:870}}
          resizeMode= 'contain'
          source = {require('./assets/homeScreen.png')}
      >
      <View style ={{paddingTop:725, paddingLeft: 80, width: "80%", height: "100%"}}>
            <Button 
              title = "Start"
            />
        </View>
      </ImageBackground>
      
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },

});
