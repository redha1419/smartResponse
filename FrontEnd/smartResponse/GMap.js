import React, {useState} from 'react';
import { StyleSheet, Text, View, Dimensions, ImageBackground, Image} from 'react-native';
import { Button } from 'react-native-elements';
import axios from 'axios'

import MapView from 'react-native-maps';

const { height, width } = Dimensions.get( 'window' );
const LATITUDE = 43.2557;
const LONGITUDE = -79.8711; 
const LATITUDE_DELTA = 0.28;
const LONGITUDE_DELTA = LATITUDE_DELTA * (width / height);

export default class GMap extends React.Component {
  constructor(props){
    super(props);
    this.fetchData = this.fetchData.bind(this);
    this.state = {
      markers:[
        /*
        {
          latitude: 45.65,
          longitude: -78.90,
          title: 'Foo Place',
          description: '1234 Foo Drive',
          image:""
        }
        */
      ],
      region: {
        latitude: LATITUDE,
        longitude: LONGITUDE,
        latitudeDelta: LATITUDE_DELTA,
        longitudeDelta: LONGITUDE_DELTA
      }
    }
  }

  fetchData(){
    axios.get('http://192.168.0.153:3001/listPoints')
    .then(response => {
      console.log("response");
      this.setState({markers: response.data.data})
      //let base64String = window.btoa(String.fromCharCode(...new Uint8Array(response.data.data.image)));
      //console.log(response.data.data[0].image);
    })
    .catch(error => {
      // handle error
      console.log(error);
      console.log('we hit an error');
    })
  }


  componentDidMount(){
    this.fetchID = setInterval(() => this.fetchData(), 5000);
    this.fetchData();
  }

  componentWillUnmount() {
    clearInterval(this.fetchID);
  }
  
  getMarkers(){
    let toReturn = [];
    for(let i=0; i<this.state.markers.length; i++){
      toReturn.push(
        <MapView.Marker
          coordinate={{latitude: parseFloat(this.state.markers[i].latitude), longitude: parseFloat(this.state.markers[i].longitude)}}
          title={this.state.markers[i].title}
          description={ this.state.markers[i].latitude + ", " + this.state.markers[i].longitude}
          key={i}
        >
          <Image source={require("./assets/sample_pic.jpg")} style={{height: 35, width:35 }} />
        </MapView.Marker>
      );
    }
    return toReturn;
  }
  render() {
    return (
      <View style={styles.container}>
        <MapView 
        style={styles.mapStyle} 
        annotations={this.state.markers} 
        initialRegion={this.state.region}>
        {this.getMarkers()}
         </MapView>
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
  mapStyle: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },
});