//
//  ExerciseInterfaceController.swift
//  HeartRateApp WatchKit Extension
//
//  Created by Monica Remer on 6/3/20.
//  Copyright © 2020 Brian Remer. All rights reserved.
//

import WatchKit
import HealthKit
import Foundation

class ExerciseInterfaceController: WKInterfaceController {

    @IBOutlet var Walking: WKInterfaceButton!
    @IBOutlet var Running: WKInterfaceButton!
    @IBOutlet var Sleeping: WKInterfaceButton!
    
    @IBOutlet var changeScreen: WKInterfaceButton!
    var exercise = ""
    
    @IBAction func walkingButtonPress() {
        exercise = "Walking"
        changeScreen.setBackgroundColor(UIColor(red: 0, green: 0, blue:255/255, alpha:1.0))
        changeScreen.setTitle("Start Walking")
    }
    
    @IBAction func runningButtonPress() {
        exercise = "Running"
        changeScreen.setBackgroundColor(UIColor(red: 0, green: 0, blue:255/255, alpha:1.0))
        changeScreen.setTitle("Start Running")
    }
    
    @IBAction func sleepingButtonPress() {
        exercise = "Sleeping"
        changeScreen.setBackgroundColor(UIColor(red: 0, green: 0, blue:255/255, alpha:1.0))
        changeScreen.setTitle("Start Sleeping")
    }
    @IBAction func changeScreenColor() {
        //changeScreen.setBackgroundColor(UIColor(red: 255/255, green: 255/255, blue: 255/255, alpha:1.0))
    }
    
    override func contextForSegue(withIdentifier segueIdentifier: String) -> Any?{
        // You may want to set the context's identifier in Interface Builder and check it here to make sure you're returning data at the proper times
        
        // Return data to be accessed in ResultsController
        return exercise
    }
    

    
}
