//
//  InterfaceController.swift
//  HeartRateApp WatchKit Extension
//
//  Created by Brian Remer on 5/25/20.
//  Copyright © 2020 Brian Remer. All rights reserved.
//
//

import WatchKit
import HealthKit
import Foundation
import WatchConnectivity

class InterfaceController: WKInterfaceController {

    
    //HealthKit Variables
    private var healthStore = HKHealthStore()
    let heartRateQuantity = HKUnit(from: "count/min")
    private var value = 0
    var queryArray = [HKAnchoredObjectQuery]()
    var dataArray = [String]()
    
    //session variables
    var session = WCSession.default//**3
    
    //button variables
    var buttonCheck = true
    var getHeartRate = false
    var exercise = ""
    
    //workout session variable
    lazy var workoutSession = startWorkout()
    
    @IBOutlet var displayTest: WKInterfaceLabel!
    @IBOutlet var startButton: WKInterfaceButton!
    @IBOutlet var bpm: WKInterfaceLabel!
    
    @IBOutlet var bpmActual: WKInterfaceLabel!
    
    
    //function for authorizing the use of the healthkit extension for the watch
    func authorizeHealthKit() {
        let healthKitTypes: Set = [
            HKObjectType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)!]
        
        healthStore.requestAuthorization(toShare: healthKitTypes, read: healthKitTypes) { (success, error) in
            
            if success {
            } else {
                print("error authorizating HealthStore. You're propably on iPad")
            }
        }
    }
 

    
    
    
    
    //function that operates based on the Start/Stop button
    @IBAction func buttonPress() {
        let stop = "Stop"
        let start = "Start"
        
        //runs if the Start button is pressed
        if(buttonCheck){
            startButton.setTitle(stop)
            startButton.setBackgroundColor(UIColor(red: 255/255, green: 0, blue:0, alpha:1.0))
            buttonCheck = false
            
            getHeartRate = true
            
            //starting the workoutsession for the watch to run in the background
            healthStore.start(workoutSession)
            
            //starting the query for the heart rate data
            queryArray.append(getCurrentHeartRateData())
        }
        //runs when the Stop button is pressed
        else{
            startButton.setTitle(start)
            startButton.setBackgroundColor(UIColor(red: 0, green: 255/255, blue:0, alpha:1.0))
            buttonCheck = true
            getHeartRate = false
            
            //goes through each active query and stops them
            for i in queryArray{
                healthStore.stop(i)
            }
            
            //This function stops the mock heart rate data from being made.
            //Only used when testing on the Xcode Simulator
            //stopMockHeartData()
            
            //creates the dictionary with the data, and then sends the dictionary from the watch to the iPhone
            let data: [String: Any] = ["watch": dataArray]
            session.sendMessage(data, replyHandler: nil, errorHandler: nil)
            
            //removes all data from the array once it has been sent
            dataArray.removeAll()
            
            //ends the workout session
            healthStore.end(workoutSession)
        }
    }
    
    //function that builds a workout session so the watch collects data in the background
    //since this only makes sure the app is continuing to work in the background, the activity and location
    //for the HKWorkoutSession does not matter
    func startWorkout() -> HKWorkoutSession{
        let configuration = HKWorkoutConfiguration()
        configuration.activityType = .running
        configuration.locationType = .outdoor
        
        
        let workoutSession = try? HKWorkoutSession(configuration: configuration)
        
        return workoutSession!
        
    }
    
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        
        //This sets the selected exercise for the data
        if let passedExercise: String = context as? String {
            exercise = passedExercise
        }
        if exercise != "" {
            bpm.setText(exercise)
        }
        
        //sets up the connectivity section
        session.delegate = self
        session.activate()
    }
    
    override func willActivate() {
        // This method is called when watch view controller is about to be visible to user
        super.willActivate()
    }
    
    override func didDeactivate() {
        // This method is called when watch view controller is no longer visible
        super.didDeactivate()
    }
    
    
    
    
    
    
    //These commented out functions are used to create random heart rate samples for the watch
    //They are only necessary to test the collection of heart rate samples on the Xcode simulator,
    //and they become uneccessary when using a physical device
    /*
    private var timer: Timer?
    
    @objc private func saveMockHeartData() {
        
        // 1. Create a heart rate BPM Sample
        let heartRateType = HKQuantityType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)!
        let heartRateQuantity = HKQuantity(unit: HKUnit(from: "count/min"),
                                           doubleValue: Double(arc4random_uniform(80) + 100))
        let heartSample = HKQuantitySample(type: heartRateType,
                                           quantity: heartRateQuantity, start: NSDate() as Date, end: NSDate() as Date)
        
        // 2. Save the sample in the store
        healthStore.save(heartSample, withCompletion: { (success, error) -> Void in
            if let error = error {
                print("Error saving heart sample: \(error.localizedDescription)")
            }
        })
    }
     */
    
    //functions that create a random heart rate sample
    /*
    @objc func writeWater() {
        guard let waterType = HKSampleType.quantityType(forIdentifier: .heartRate) else {
            print("Sample type not available")
            return
        }
        
        let waterQuantity = HKQuantity(unit: HKUnit(from: "count/min"), doubleValue: Double(arc4random_uniform(80) + 100))
        let today = Date()
        let waterQuantitySample = HKQuantitySample(type: waterType, quantity: waterQuantity, start: today, end: today)
        
        HKHealthStore().save(waterQuantitySample) { (success, error) in
            //print("HK write finished - success: \(success); error: \(error)")
            //self.readWater()
        }
    }
    
    private func startMockHeartData() {
        timer = Timer.scheduledTimer(timeInterval: 1.0,
                                                       target: self,
                                                       selector: #selector(writeWater),
                                                       userInfo: nil,
                                                       repeats: true)
    }
    private func stopMockHeartData() {
        self.timer?.invalidate()
    }
 */
    
    
    
    //Heart Rate Data query variables
    var currentHeartRateSample : [HKSample]?
    
    var currentHeartLastSample : HKSample?
    
    var currentHeartRateBPM = Double()
    
    //This function gets continuous heart rate samples from the watch once it is called
    func getCurrentHeartRateData() -> HKAnchoredObjectQuery{
        
        let calendar = Calendar.current
        let components = calendar.dateComponents([.year, .month, .day], from: Date())
        let startDate : Date = calendar.date(from: components)!
        let endDate : Date = calendar.date(byAdding: Calendar.Component.day, value: 1, to: startDate as Date)!
        
        let sampleType : HKSampleType =  HKObjectType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)!
        let predicate : NSPredicate =  HKQuery.predicateForSamples(withStart: startDate, end: endDate, options: [])
        let anchor: HKQueryAnchor = HKQueryAnchor(fromValue: 0)
        
        let anchoredQuery = HKAnchoredObjectQuery(type: sampleType, predicate: predicate, anchor: anchor, limit: HKObjectQueryNoLimit) { (query, samples, deletedObjects, anchor, error ) in
            
            if samples != nil {
                
                self.collectCurrentHeartRateSample(currentSampleTyple: samples!, deleted: deletedObjects!)
                
            }
            
        }
        
        anchoredQuery.updateHandler = { (query, samples, deletedObjects, anchor, error) -> Void in
            self.collectCurrentHeartRateSample(currentSampleTyple: samples!, deleted: deletedObjects!)
        }
        
        
        self.healthStore.execute(anchoredQuery)
        return anchoredQuery
        
        
    }
    
    //gets the specific heart rate value from the current sample
    func collectCurrentHeartRateSample(currentSampleTyple : [HKSample]?, deleted : [HKDeletedObject]?){
        
        self.currentHeartRateSample = currentSampleTyple
        
        //Get Last Sample of Heart Rate
        self.currentHeartLastSample = self.currentHeartRateSample?.last
        
        if self.currentHeartLastSample != nil {
            let lastHeartRateSample = self.currentHeartLastSample as! HKQuantitySample
            
            self.currentHeartRateBPM = lastHeartRateSample.quantity.doubleValue(for: HKUnit(from: "count/min"))
            
            bpmActual.setText(String(currentHeartRateBPM))
            dataArray.append(exercise + "," + String(currentHeartRateBPM) + "\n")
            
        }
        
    }
    
    
    
    
   
    
    
    
    
    
    

    

}

extension InterfaceController: WCSessionDelegate {
    
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
    }
    
    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
        
        //print("received data: \(message)")
        //if let value = message["iPhone"] as? String {//**7.1
            //self.label.setText(value)
        //}
    }
}
