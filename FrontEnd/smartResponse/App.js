import {createAppContainer} from 'react-navigation';
import {createStackNavigator} from 'react-navigation-stack';
import 'react-native-gesture-handler';
import Welcome from './Welcome.js'
import GMap from './GMap.js'

const MainNavigator = createStackNavigator(
  {
  Home: {screen: Welcome},
  Map: {screen: GMap},
  },
  {
    initialRouteName: 'Home',
  }
);

const App = createAppContainer(MainNavigator);

export default App;