//
//  Calender.swift
//  Pinky
//
//  Created by 山川拓也 on 2018/10/27.
//  Copyright © 2018 山川拓也. All rights reserved.
//
import EventKit

class Calender {
    // EventStoreを初期化
    let eventStore = EKEventStore()
    
    // 許可状況を確認して、許可されていなかったら許可を得る
    func allowAuthorization() {
        if getAuthorization_status() {
            // 許可されている
            return
        } else {
            // 許可されていない
            eventStore.requestAccess(to: .event, completion: {
                (granted, error) in
                if granted {
                    return
                }
                else {
                    print("Not allowed")
                }
            })
            
        }
    }
    
    // 認証ステータスを確認する
    func getAuthorization_status() -> Bool {
        // 認証ステータスを取得
        let status = EKEventStore.authorizationStatus(for: .event)
        
        // ステータスを表示 許可されている場合のみtrueを返す
        switch status {
        case .notDetermined:
            print("NotDetermined")
            return false
            
        case .denied:
            print("Denied")
            return false
            
        case .authorized:
            print("Authorized")
            return true
            
        case .restricted:
            print("Restricted")
            return false
        
        }
    }
    
    func addEvent(limited_at: String, title: String, endDate: String) {
        // イベントの情報を準備
        let startDate = NSDate()
        let cal = NSCalendar(identifier: NSCalendar.Identifier.gregorian)!
        let defaultCalendar = eventStore.defaultCalendarForNewEvents
        
        let dateFormater = DateFormatter()
        dateFormater.locale = Locale(identifier: "ja_JP")
        dateFormater.dateFormat = "yyyy/MM/dd HH:mm:ss"
        let edate = dateFormater.date(from: endDate)
        
        // イベントを作成して情報をセット
        let event = EKEvent(eventStore: eventStore)
        event.title = title
        event.startDate = startDate as Date
        event.endDate = edate
        event.calendar = defaultCalendar
        // イベントの登録
        do {
            try eventStore.save(event, span: .thisEvent)
        } catch let error {
            print(error)
        }
    }
    
//    func listEvents() {
//        // 検索条件を準備
//        let startDate = NSDate()
//        let endDate = NSDate()
//        let defaultCalendar = eventStore.defaultCalendarForNewEvents    // ここではデフォルトのカレンダーを指定
//
//        // 検索するためのクエリー的なものを用意
//        let predicate = eventStore.predicateForEvents(withStart: startDate as Date, end: endDate as Date, calendars: [defaultCalendar!])
//        // イベントを検索
//        let events = eventStore.events(matching: predicate)
//
//        print(events)
//    }
}
