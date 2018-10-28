//
//  TimeLine.swift
//  Pinky
//
//  Created by 山川拓也 on 2018/10/26.
//  Copyright © 2018 山川拓也. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON
import AlamofireImage

class TimeLine: UIViewController, UITableViewDelegate, UITableViewDataSource{
    
    @IBOutlet weak var timeline: UITableView!
    
    let url = "https://pinky.kentaiwami.jp/promise/9"
    let myID = 9 //仮ID
    
    var pro : [Promise] = []
    var count = true
    var count2 = true
    private weak var refreshControl: UIRefreshControl!
    
    var transRotate = CGAffineTransform()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        initializePullToRefresh()
        
        self.timeline.delegate = self
        self.timeline.dataSource = self
        
        callAPI()
//        let calender = Calender()
//        calender.listEvents()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        let titleview = UIImageView(image: UIImage(named: "pinky_header"))
        self.navigationItem.titleView = titleview
        //refresh()
    }

    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return pro.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "TimeLineCell") as! TimeLineCell
        
        cell.profileName.text = pro[indexPath.row].name
        cell.profileName.layer.masksToBounds = true
        cell.profileName.layer.cornerRadius = 10
        cell.profileName.layer.maskedCorners = [.layerMinXMaxYCorner, .layerMaxXMaxYCorner]
        
        cell.promise.text = pro[indexPath.row].content
        cell.DateTime.text = pro[indexPath.row].created_at + "に約束しました"
        
        if pro[indexPath.row].limited_at == "" {
            cell.deliver.text = "期限なし"
        }else{
            cell.deliver.text = pro[indexPath.row].limited_at
        }

        if pro[indexPath.row].is_master {
            cell.promiseArrow.image = UIImage(named: "right")
        }else{
             cell.promiseArrow.image = UIImage(named: "left")
        }
        
        let filter = AspectScaledToFillSizeWithRoundedCornersFilter(
            size: cell.profileImg.frame.size,
            radius: 10.0
        )
        cell.profileImg.af_setImage(withURL: URL(string: pro[indexPath.row].img)!, filter: filter)
        
        if pro[indexPath.row].one_side_done == 0 {
            cell.compLabel.isHidden = true
        }else{
            if pro[indexPath.row].one_side_done == myID{
                self.count = false
            }else{
                self.count = true
            }
            cell.compLabel.isHidden = false
        }
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        // タップ時の処理を記述
        
    }
    
    @available(iOS 11.0, *)
    func tableView(_ tableView: UITableView, trailingSwipeActionsConfigurationForRowAt indexPath: IndexPath) -> UISwipeActionsConfiguration? {
        
            let check =  UIContextualAction(style: .normal, title: "Check", handler: { (action,view,completionHandler ) in
                //do stuff
                
                if self.pro[indexPath.row].one_side_done == 0 {
                    self.count = false
                    
                    self.putAPI(user_id: self.myID, index: indexPath.row)
                }else{
                    if self.pro[indexPath.row].one_side_done == self.myID{
                        self.show_alert(index: indexPath.row)
                    }else{
                        self.count = false
                        
                        self.putAPI(user_id: self.myID, index: indexPath.row)
                    }
                    
                }
                
                if self.pro[indexPath.row].one_side_done == 0 {
                    self.count = false
                    
                    self.putAPI(user_id: self.myID, index: indexPath.row)
                }else{
                    self.show_alert(index: indexPath.row)
                    
                }

                completionHandler(true)
            })
        
        
        if pro[indexPath.row].one_side_done == 0 {
            check.title = "Check"
            check.image = UIImage(named: "check")
            check.backgroundColor = UIColor(hex: "DB4F4A")
        }else{
            if pro[indexPath.row].one_side_done == myID{
                self.count = false
                check.title = "Checked"
                check.image = UIImage(named: "cancel")
                check.backgroundColor = UIColor(hex: "4A4A4A")
            }else{
                self.count = true
                check.title = "Check"
                check.image = UIImage(named: "check")
                check.backgroundColor = UIColor(hex: "DB4F4A")
            }
            
        }
        
        let confrigation = UISwipeActionsConfiguration(actions: [check])
        
        return confrigation
    }
    
    func callAPI(){
        Alamofire.request(url)
            .responseJSON{res in
                
                let json = JSON(res.value)
                let list = json["results"].arrayValue
                (0 ..< list.count).forEach { (i) in
                    var tmp = Promise(id: list[i]["id"].intValue,
                                    content: list[i]["content"].stringValue,
                                      calender_date: list[i]["calender_date"].stringValue,
                                      created_at: list[i]["created_at"].stringValue,
                                      img: list[i]["img"].stringValue,
                                      is_master: list[i]["is_master"].boolValue,
                                      limited_at: list[i]["limited_at"].stringValue,
                                      one_side_done: list[i]["one_side_done"].intValue,
                                      name: list[i]["name"].stringValue
                    )
                    self.pro.append(tmp)
                }
                self.timeline.reloadData()
        }
    }
    
    func show_alert(index: Int) {
        let alert: UIAlertController = UIAlertController(title: "達成の取り消し", message: "取り消しますか？", preferredStyle:  UIAlertController.Style.alert)
        

        let defaultAction: UIAlertAction = UIAlertAction(title: "はい", style: UIAlertAction.Style.default, handler:{
            // ボタンが押された時の処理を書く（クロージャ実装）
            (action: UIAlertAction!) -> Void in
            self.count = true
            self.putAPI(user_id: -1, index: index)
            print("OK")
        })
        // キャンセルボタン
        let cancelAction: UIAlertAction = UIAlertAction(title: "キャンセル", style: UIAlertAction.Style.cancel, handler:{
            // ボタンが押された時の処理を書く（クロージャ実装）
            (action: UIAlertAction!) -> Void in
            self.count = false
            print("Cancel")
        })
        
        alert.addAction(cancelAction)
        alert.addAction(defaultAction)
        
        present(alert, animated: true, completion: nil)
    }
    
    func putAPI(user_id: Int, index: Int) {
        let putURL = "https://pinky.kentaiwami.jp/promise"
        let params = [
            "user_id": user_id,
            "promise_id": self.pro[index].id
        ]
        
        Alamofire.request(
            putURL,
            method: .put,
            parameters: params,
            encoding: JSONEncoding(options: [])).responseJSON {
                (response) in
                // レスポンスの結果を受け取る(Any型)
                print(response.value)
        }
        self.refresh()
    }
    
    /********************* Pull to refresh関連 *********************/
    private func initializePullToRefresh() {
        let control = UIRefreshControl()
        control.addTarget(self, action: #selector(onPullToRefresh(_:)), for: .valueChanged)
        timeline.addSubview(control)
        refreshControl = control
    }
    
    @objc private func onPullToRefresh(_ sender: AnyObject) {
        refresh()
        
    }
    
    private func stopPullToRefresh() {
        if refreshControl.isRefreshing {
            refreshControl.endRefreshing()
        }
    }
    
    private func refresh() {
        DispatchQueue.global().async {
            Thread.sleep(forTimeInterval: 1.0)
            DispatchQueue.main.async {
                self.completeRefresh()
            }
        }
    }
    
    private func completeRefresh() {
        stopPullToRefresh()
        self.pro.removeAll()
        callAPI()
        timeline.reloadData()
//        let calender = Calender()
//        calender.addEvent(limited_at: <#T##String#>, title: <#T##String#>, endDate: <#T##String#>)
    }
    /********************************************************/
}
