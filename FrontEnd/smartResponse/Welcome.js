import React, {useState} from 'react';
import { StyleSheet, Text, View, ImageBackground} from 'react-native';
import { Button } from 'react-native-elements';

export default class Welcome extends React.Component {
  render(){
    const {navigate} = this.props.navigation;
    return (
      <View style={{}}>

      <ImageBackground
          style = {{width:'100%', height:'100%'}} source = {require('./assets/homeScreen.png')}>
      <View style ={{paddingTop:530, paddingLeft: 0, width: "100%", height: "100%"}}>
            <Button 
              title = "Start"
              onPress={() => navigate('Map')}
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
